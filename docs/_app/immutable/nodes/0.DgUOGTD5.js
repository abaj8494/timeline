import{d as g,e as k,c as w,a as v,t as $}from"../chunks/CB0lZw64.js";import{W as T,h,v as y,ac as E,af as A,F as _,Q as R,ag as N,ah as P,z as S,R as u,t as C,E as O,C as j,J as q,ai as z,p as F,o as I,a0 as b,a as L,a7 as H,X as M}from"../chunks/EIGgl-ut.js";import{h as W}from"../chunks/CKoSanPy.js";import{s as X,a as D}from"../chunks/BPP8tfC-.js";import{p as J}from"../chunks/CxhrW5hK.js";import{g as n,b as c}from"../chunks/CKmWNKX5.js";function K(p,l,i=!1,s=!1,f=!1){var a=p,m="";T(()=>{var t=E;if(m===(m=l()??"")){h&&y();return}if(t.nodes_start!==null&&(A(t.nodes_start,t.nodes_end),t.nodes_start=t.nodes_end=null),m!==""){if(h){_.data;for(var e=y(),r=e;e!==null&&(e.nodeType!==8||e.data!=="");)r=e,e=R(e);if(e===null)throw N(),P;g(_,r),a=S(e);return}var d=m+"";i?d=`<svg>${d}</svg>`:s&&(d=`<math>${d}</math>`);var o=k(d);if((i||s)&&(o=u(o)),g(u(o),o.lastChild),i||s)for(;u(o);)a.before(u(o));else a.before(o)}})}function Q(p,l,...i){var s=p,f=q,a;C(()=>{f!==(f=l())&&(a&&(z(a),a=null),a=j(()=>f(s,...i)))},O),h&&(s=_)}const U=!0,ae=Object.freeze(Object.defineProperty({__proto__:null,prerender:U},Symbol.toStringTag,{value:"Module"}));var Y=$('<meta name="description" content="Explore history through an interactive timeline of influential people, books, and artworks"> <!>',1);function te(p,l){F(l,!0);const[i,s]=X(),f=()=>D(J,"$page",i);I(()=>{function t(e){if(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA")return;const r=f().url.pathname;switch(e.key.toLowerCase()){case"s":n(`${c}/search`);break;case"b":r.includes("/books")||n(`${c}/books`);break;case"a":r.includes("/artworks")||n(`${c}/artworks`);break;case"l":n(`${c}/list`);break;case"p":r.includes("/people")||n(`${c}/people`);break;case"c":r.includes("/cosmic")||n(`${c}/cosmic`);break;case"h":r.includes("/humanity")||n(`${c}/humanity`);break}}return window.addEventListener("keydown",t),()=>{window.removeEventListener("keydown",t)}});var a=w();W(t=>{var e=Y();H.title="Timeline - Interactive Historical Timeline";var r=M(b(e),2);K(r,()=>`<script type="application/ld+json">
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
	<\/script>`),v(t,e)});var m=b(a);Q(m,()=>l.children),v(p,a),L(),s()}export{te as component,ae as universal};
