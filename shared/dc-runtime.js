/*
 * dc-runtime.js — a tiny standalone runtime for the simulator pages.
 *
 * Each page has:
 *   <template id="dc-template"> … markup with {{holes}}, <sc-for>, <sc-if> … </template>
 *   <script type="text/x-dc" data-dc-script> class Component extends DCLogic { … } </script>
 *
 * The runtime evaluates the Component class, calls renderVals() on every state
 * change, renders the template against the returned values and patches the live
 * DOM in place (so sliders keep working while you drag them).
 *
 * Template features supported:
 *   {{ a.b.c }}               dotted lookup (or a literal: true, false, null, numbers, 'strings')
 *   attr="{{ x }}"            raw value (functions become event handlers for on* attributes)
 *   attr="a {{x}} b"          interpolated string
 *   onClick / onChange / onInput="{{ fn }}"
 *   <sc-for list="{{xs}}" as="item">   repeats children; {{item.*}} and {{$index}} in scope
 *   <sc-if value="{{cond}}">           renders children when truthy
 */
(function () {
  'use strict';

  // ---------- component base class ----------
  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
  }
  DCLogic.prototype.setState = function (partial) {
    var next = typeof partial === 'function' ? partial(this.state, this.props) : partial;
    if (next) for (var k in next) this.state[k] = next[k];
    if (this.__schedule) this.__schedule();
  };
  DCLogic.prototype.forceUpdate = function () {
    if (this.__schedule) this.__schedule();
  };
  window.DCLogic = DCLogic;

  // ---------- value lookup ----------
  var HOLE = /\{\{\s*([^}]*?)\s*\}\}/g;
  var WHOLE = /^\s*\{\{\s*([^}]*?)\s*\}\}\s*$/;

  function lookup(expr, scope) {
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (expr === 'undefined' || expr === '') return undefined;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return parseFloat(expr);
    var q = expr.match(/^(['"])(.*)\1$/);
    if (q) return q[2];
    var parts = expr.split('.');
    var v = scope;
    for (var i = 0; i < parts.length; i++) {
      if (v === null || v === undefined) return undefined;
      v = v[parts[i]];
    }
    return v;
  }

  function interpolate(str, scope) {
    return str.replace(HOLE, function (_, expr) {
      var v = lookup(expr, scope);
      return v === null || v === undefined ? '' : String(v);
    });
  }

  function evalAttr(raw, scope) {
    var m = raw.match(WHOLE);
    if (m) return lookup(m[1], scope);
    if (raw.indexOf('{{') === -1) return raw;
    return interpolate(raw, scope);
  }

  // ---------- virtual nodes ----------
  // { t: 'text', v } | { t: 'el', ns, tag, attrs: {}, props: {}, on: {}, kids: [] }

  var BOOL_PROPS = { checked: 1, disabled: 1, selected: 1 };
  var EVENT_ATTRS = { onclick: 'click', onchange: 'change', oninput: 'input', onpointerdown: 'pointerdown', onpointerup: 'pointerup', onpointermove: 'pointermove' };

  function build(node, scope, out) {
    if (node.nodeType === 3) {
      var text = node.nodeValue;
      out.push({ t: 'text', v: text.indexOf('{{') === -1 ? text : interpolate(text, scope) });
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.localName;

    if (tag === 'sc-for') {
      var list = evalAttr(node.getAttribute('list') || '', scope) || [];
      var as = node.getAttribute('as') || 'item';
      for (var i = 0; i < list.length; i++) {
        var child = Object.create(scope);
        child[as] = list[i];
        child.$index = i;
        buildKids(node, child, out);
      }
      return;
    }
    if (tag === 'sc-if') {
      if (evalAttr(node.getAttribute('value') || '', scope)) buildKids(node, scope, out);
      return;
    }

    var v = { t: 'el', ns: node.namespaceURI, tag: tag, attrs: {}, props: {}, on: {}, kids: [] };
    for (var a = 0; a < node.attributes.length; a++) {
      var at = node.attributes[a];
      var name = at.name;
      if (name.indexOf('hint-') === 0) continue;
      var lname = name.toLowerCase();
      var val = evalAttr(at.value, scope);
      if (EVENT_ATTRS[lname]) {
        if (typeof val === 'function') v.on[lname] = val;
        continue;
      }
      if (BOOL_PROPS[lname]) {
        v.props[lname] = !!val && val !== 'false';
        continue;
      }
      if (lname === 'value' && (tag === 'input' || tag === 'textarea' || tag === 'select')) {
        v.props.value = val === null || val === undefined ? '' : String(val);
        v.attrs.value = v.props.value;
        continue;
      }
      if (val === false || val === null || val === undefined) continue;
      v.attrs[name] = String(val);
    }
    buildKids(node, scope, v.kids);
    out.push(v);
  }

  function buildKids(node, scope, out) {
    var src = node.content || node; // <template> content
    for (var c = src.firstChild; c; c = c.nextSibling) build(c, scope, out);
  }

  // ---------- DOM creation and patching ----------
  function eventType(el, attr) {
    if (attr === 'onchange') {
      var type = (el.getAttribute('type') || '').toLowerCase();
      // React-style onChange: fire continuously for text and range inputs
      if (el.localName === 'input' && type !== 'checkbox' && type !== 'radio') return 'input';
      if (el.localName === 'textarea') return 'input';
      return 'change';
    }
    return EVENT_ATTRS[attr];
  }

  function setHandlers(el, on) {
    var old = el.__dcOn || {};
    el.__dcOn = on;
    for (var k in on) {
      if (!old[k] && !(el.__dcBound && el.__dcBound[k])) {
        el.__dcBound = el.__dcBound || {};
        el.__dcBound[k] = true;
        (function (key) {
          el.addEventListener(eventType(el, key), function (e) {
            var h = el.__dcOn && el.__dcOn[key];
            if (h) h(e);
          });
        })(k);
      }
    }
  }

  function create(v) {
    if (v.t === 'text') return document.createTextNode(v.v);
    var el = v.ns ? document.createElementNS(v.ns, v.tag) : document.createElement(v.tag);
    for (var k in v.attrs) el.setAttribute(k, v.attrs[k]);
    for (var p in v.props) el[p] = v.props[p];
    setHandlers(el, v.on);
    for (var i = 0; i < v.kids.length; i++) el.appendChild(create(v.kids[i]));
    return el;
  }

  function same(dom, v) {
    if (v.t === 'text') return dom.nodeType === 3;
    return dom.nodeType === 1 && dom.localName === v.tag && dom.namespaceURI === (v.ns || dom.namespaceURI);
  }

  function patchEl(el, v) {
    var cur = el.attributes;
    for (var i = cur.length - 1; i >= 0; i--) {
      var n = cur[i].name;
      if (!(n in v.attrs)) el.removeAttribute(n);
    }
    for (var k in v.attrs) {
      if (el.getAttribute(k) !== v.attrs[k]) el.setAttribute(k, v.attrs[k]);
    }
    for (var p in v.props) {
      if (p === 'value') {
        if (el.value !== v.props.value && document.activeElement !== el) el.value = v.props.value;
        else if (el.value !== v.props.value && el.type !== 'range') el.value = v.props.value;
      } else if (el[p] !== v.props[p]) el[p] = v.props[p];
    }
    setHandlers(el, v.on);
    patchKids(el, v.kids);
  }

  function patchKids(parent, kids) {
    var dom = parent.firstChild;
    for (var i = 0; i < kids.length; i++) {
      var v = kids[i];
      if (!dom) {
        parent.appendChild(create(v));
        continue;
      }
      var next = dom.nextSibling;
      if (same(dom, v)) {
        if (v.t === 'text') {
          if (dom.nodeValue !== v.v) dom.nodeValue = v.v;
        } else patchEl(dom, v);
      } else {
        parent.replaceChild(create(v), dom);
      }
      dom = next;
    }
    while (dom) {
      var n2 = dom.nextSibling;
      parent.removeChild(dom);
      dom = n2;
    }
  }

  // ---------- boot ----------
  function boot() {
    var tpl = document.getElementById('dc-template');
    var scriptEl = document.querySelector('script[data-dc-script]');
    var mount = document.getElementById('dc-root');
    if (!tpl || !scriptEl || !mount) return;

    var Component;
    try {
      Component = new Function('DCLogic', scriptEl.textContent + '\n;return Component;')(DCLogic);
    } catch (err) {
      mount.textContent = 'Simulator failed to load: ' + err.message;
      throw err;
    }

    var inst = new Component({});
    if (!inst.state) inst.state = {};
    var queued = false;

    function render() {
      queued = false;
      var vals = inst.renderVals ? inst.renderVals() || {} : {};
      var out = [];
      buildKids(tpl, vals, out);
      patchKids(mount, out);
    }
    inst.__schedule = function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(render);
    };

    render();
    if (inst.componentDidMount) inst.componentDidMount();
    window.addEventListener('pagehide', function () {
      if (inst.componentWillUnmount) inst.componentWillUnmount();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
