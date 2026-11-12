// Static-site data layer: answers api() GETs from the JSON files exported by scripts/build_static.py
// (api/info.json, api/course.json, api/readme.json, api/data.json, api/lesson/<id>.json). POST /python/<name> runs
// the course scripts in Python, so it is refused here; the lesson pages hide "Check with Python" on the static site.
const files = new Map();
function file(rel) {
  if (!files.has(rel)) {
    files.set(rel, fetch('api/' + rel + '.json').then(r => { if (!r.ok) throw new Error(`${r.status} ${rel}`); return r.json(); }));
  }
  return files.get(rel);
}

export async function staticApi(path, body) {
  const clean = path.split('?')[0].replace(/^\/+/, '');
  if (body || clean.startsWith('python')) throw new Error('Running the Python scripts needs the local app (python run_web.py).');
  return file(clean);
}
