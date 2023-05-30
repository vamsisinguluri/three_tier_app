export default { set }

function set(r) {
  var fs = require('fs');

  try {
    var c =  fs.readFileSync("/etc/nginx/conf.d/active.txt");
  } catch (e) {
    r.error("Error while reading upstrem file.");
    // maybe set c to somehting default then.
  }
  return c;
}