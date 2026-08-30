const crypto = require('crypto-js');

const qc = {
    aes: function encrypt(params) {
    const text = typeof params.data === "string"
        ? params.data
        : JSON.stringify(params.data)

    const data = crypto.enc.Utf8.parse(text)
    const key = crypto.enc.Utf8.parse(params.aesKey)

    return crypto.AES.encrypt(data, key, {
        mode: crypto.mode.ECB,
        padding: crypto.pad.Pkcs7,
    }).toString()
},
    zxzq: {
        uuid: function get_uuid(n) {
            const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("");
            let res = "";
            for (let i = 0; i < 32; i++) {
                res += chars[Math.floor(Math.random() * 62)];
            }
            return res;
        },
        cb: function get_cb() {
            let a0 = {
                "suffix": "m25b40",
                "code": "vfnv46",
                "pos": [
                    1,
                    10,
                    12,
                    13,
                    26,
                    31
                ]
            };
            _0x86f269 = _0x183b74["code"];
            _0x22d54d = a0['pos'];
            for (var _0x56eeac = this.uuid(0x20).split(''), _0x3d43fc = 0x0; _0x3d43fc < 6, _0x3d43fc++;) {
                _0x56eeac[_0x22d54d[_0x3d43fc]] = _0x86f269['charAt'](_0x3d43fc);
                _0x58ee17 = _0x56eeac.join('');
            }
            return _0xb77ce(_0x58ee17);
        }
    }
    
}





module.exports =  qc;

