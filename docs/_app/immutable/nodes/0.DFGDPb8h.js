import{d as g,e as k,c as w,a as b,t as $}from"../chunks/tV2K8-t_.js";import{o as T}from"../chunks/uz48rOOJ.js";import{_ as E,v as h,x as v,ad as A,aF as S,I as _,M as N,aC as R,aB as P,B as C,N as d,w as F,E as I,F as O,r as j,an as q,p as L,Z as y,a as M,a2 as z,a1 as B}from"../chunks/WXaAkZrh.js";import{h as H}from"../chunks/DcaoexEE.js";import{s as D,a as K}from"../chunks/CVG9xlgL.js";import{s as U,g as u}from"../chunks/CN0F17v8.js";import{b as m}from"../chunks/Bh0SCLq4.js";function W(t,n,o=!1,s=!1,l=!1){var a=t,p="";E(()=>{var r=A;if(p===(p=n()??"")){h&&v();return}if(r.nodes_start!==null&&(S(r.nodes_start,r.nodes_end),r.nodes_start=r.nodes_end=null),p!==""){if(h){_.data;for(var e=v(),i=e;e!==null&&(e.nodeType!==8||e.data!=="");)i=e,e=N(e);if(e===null)throw R(),P;g(_,i),a=C(e);return}var f=p+"";o?f=`<svg>${f}</svg>`:s&&(f=`<math>${f}</math>`);var c=k(f);if((o||s)&&(c=d(c)),g(d(c),c.lastChild),o||s)for(;d(c);)a.before(d(c));else a.before(c)}})}function X(t,n,...o){var s=t,l=j,a;F(()=>{l!==(l=n())&&(a&&(q(a),a=null),a=O(()=>l(s,...o)))},I),h&&(s=_)}const Y=!0,se=Object.freeze(Object.defineProperty({__proto__:null,prerender:Y},Symbol.toStringTag,{value:"Module"})),Z=()=>{const t=U;return{page:{subscribe:t.page.subscribe},navigating:{subscribe:t.navigating.subscribe},updated:t.updated}},G={subscribe(t){return Z().page.subscribe(t)}};var J=$('<meta name="description" content="Explore history through an interactive timeline of influential people and books"> <!>',1);function ne(t,n){L(n,!0);const[o,s]=D(),l=()=>K(G,"$page",o);T(()=>{function r(e){if(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA")return;const i=l().url.pathname;switch(e.key.toLowerCase()){case"s":u(`${m}/search`);break;case"b":i.includes("/books")||u(`${m}/books`);break;case"l":u(`${m}/list`);break;case"p":i.includes("/people")||u(`${m}/people`);break}}return window.addEventListener("keydown",r),()=>{window.removeEventListener("keydown",r)}});var a=w();H(r=>{var e=J();z.title="Shrine - Interactive Historical Timeline";var i=B(y(e),2);W(i,()=>`<script type="application/ld+json">
	{
		"@context": "https://schema.org",
		"@type": "WebSite",
		"name": "Shrine Timeline",
		"description": "An interactive timeline visualization of historical figures and influential books throughout history",
		"url": "https://yourdomain.com/shrine/",
		"potentialAction": {
			"@type": "SearchAction",
			"target": "https://yourdomain.com/shrine/search?q={search_term_string}",
			"query-input": "required name=search_term_string"
		}
	}
	<\/script>`),b(r,e)});var p=y(a);X(p,()=>n.children),b(t,a),M(),s()}export{ne as component,se as universal};
