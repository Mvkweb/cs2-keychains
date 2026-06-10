browser.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (details.method === "POST" && details.requestBody && details.requestBody.raw) {
            try {
                // The payload is in raw bytes, convert to string
                const rawBytes = details.requestBody.raw[0].bytes;
                const bodyStr = new TextDecoder("utf-8").decode(rawBytes);
                
                const parsedBody = JSON.parse(bodyStr);
                if (Array.isArray(parsedBody) && parsedBody.length > 0) {
                    const item = parsedBody[0];
                    if ('kc_x2' in item) {
                        const payload = {
                            kc_x2: item.kc_x2,
                            kc_y2: item.kc_y2,
                            kc_z2: item.kc_z2
                        };
                        
                        // Send it securely to our Python server running in the terminal!
                        fetch('http://127.0.0.1:5000/copy-charm', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        }).then(() => console.log("Sent coords to Python server!"))
                          .catch(e => console.error("Python server not running!", e));
                    }
                }
            } catch (e) {
                // Ignore parse errors for unrelated POST requests
            }
        }
    },
    { urls: ["*://api.cs2inspects.com/getFakeInspectLink2*"] },
    ["requestBody"]
);
