import{d as g,e as k,c as w,a as b,t as $}from"../chunks/tV2K8-t_.js";import{o as T}from"../chunks/uz48rOOJ.js";import{_ as E,v as _,x as v,ad as A,aF as N,I as h,M as R,aC as S,aB as P,B as C,N as m,w as F,E as I,F as O,r as j,an as q,p as L,Z as y,a as M,a2 as z,a1 as B}from"../chunks/WXaAkZrh.js";import{h as H}from"../chunks/DcaoexEE.js";import{s as D,a as K}from"../chunks/CVG9xlgL.js";import{s as U,g as u}from"../chunks/BvkaOCK-.js";import{b as d}from"../chunks/kwNBNGnL.js";function W(t,n,i=!1,s=!1,l=!1){var a=t,p="";E(()=>{var r=A;if(p===(p=n()??"")){_&&v();return}if(r.nodes_start!==null&&(N(r.nodes_start,r.nodes_end),r.nodes_start=r.nodes_end=null),p!==""){if(_){h.data;for(var e=v(),o=e;e!==null&&(e.nodeType!==8||e.data!=="");)o=e,e=R(e);if(e===null)throw S(),P;g(h,o),a=C(e);return}var f=p+"";i?f=`<svg>${f}</svg>`:s&&(f=`<math>${f}</math>`);var c=k(f);if((i||s)&&(c=m(c)),g(m(c),c.lastChild),i||s)for(;m(c);)a.before(m(c));else a.before(c)}})}function X(t,n,...i){var s=t,l=j,a;F(()=>{l!==(l=n())&&(a&&(q(a),a=null),a=O(()=>l(s,...i)))},I),_&&(s=h)}const Y=!0,se=Object.freeze(Object.defineProperty({__proto__:null,prerender:Y},Symbol.toStringTag,{value:"Module"})),Z=()=>{const t=U;return{page:{subscribe:t.page.subscribe},navigating:{subscribe:t.navigating.subscribe},updated:t.updated}},G={subscribe(t){return Z().page.subscribe(t)}};var J=$('<meta name="description" content="Explore history through an interactive timeline of influential people, books, and artworks"> <!>',1);function oe(t,n){L(n,!0);const[i,s]=D(),l=()=>K(G,"$page",i);T(()=>{function r(e){if(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA")return;const o=l().url.pathname;switch(e.key.toLowerCase()){case"s":u(`${d}/search`);break;case"b":o.includes("/books")||u(`${d}/books`);break;case"a":o.includes("/artworks")||u(`${d}/artworks`);break;case"l":u(`${d}/list`);break;case"p":o.includes("/people")||u(`${d}/people`);break}}return window.addEventListener("keydown",r),()=>{window.removeEventListener("keydown",r)}});var a=w();H(r=>{var e=J();z.title="Timeline - Interactive Historical Timeline";var o=B(y(e),2);W(o,()=>`<script type="application/ld+json">
	{
		"@context": "https://schema.org",
		"@type": "WebSite",
		"name": "Timeline",
		"description": "An interactive timeline visualization of historical figures, influential books, and famous artworks throughout history",
		"url": "https://yourdomain.com/timeline/",
		"potentialAction": {
			"@type": "SearchAction",
			"target": "https://yourdomain.com/timeline/search?q={search_term_string}",
			"query-input": "required name=search_term_string"
		}
	}
	<\/script>`),b(r,e)});var p=y(a);X(p,()=>n.children),b(t,a),M(),s()}export{oe as component,se as universal};
