// Prefix a site-root path with the deployment base, so the same links work at
// https://daviddef.github.io/TheDefranceski/ and at https://defranceski.com/.
const BASE = import.meta.env.BASE_URL.replace(/\/$/, "");
/* 16 October 2026. Every page of this site lives at /x/, so a link to /x costs
   the reader a redirect (the audit counted 14,410 of them). This is the one
   function every template and every kit component builds its links with, so
   the slash is added here: to a path with no file extension, before any ?query
   or #fragment. Files (.css, .json, .jpg) and paths already ending in / are
   untouched. */
const slashed = (p) => {
  const m = /^([^?#]*)([?#][\s\S]*)?$/.exec(p);
  const path = m[1], rest = m[2] || "";
  return path === "" || path.endsWith("/") || /\.[A-Za-z0-9]{1,6}$/.test(path) ? p : path + "/" + rest;
};
export const u = (p = "/") => `${BASE}${slashed(p.startsWith("/") ? p : "/" + p)}`;

// A hand-written data string once carried the template expression itself,
// href={u("/corrections/")}, and the page printed it as the link target. Data
// files hold plain HTML, not template code: turn that shape into an ordinary
// root-relative href, which the family renderers then base like any other.
export const plainHref = (html) =>
  String(html ?? "").replace(/href=\{u\(\s*(["'])(.*?)\1\s*\)\}/g, 'href="$2"');
