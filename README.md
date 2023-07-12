# tosilk

tosilk is a online [silk-v3-decoder](https://github.com/kn007/silk-v3-decoder) server

You can convert between silk and MP3 through the interface of decoder and encoder

## Demo (not long-term support)

[https://tosilk.zeabur.app/docs](https://tosilk.zeabur.app/docs)



## Quickly Usage
Use the following command to convert your MP3 file to Silk format:

### decoder
```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "base64": "<your_mp3_base64>",
  "url": "<your_mp3_url>"
}' "https://tosilk.zeabur.app/v1/decoder"
```

### encoder
```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "base64": "<your_mp3_base64>",
  "url": "<your_mp3_url>"
}' "https://tosilk.zeabur.app/v1/encoder"
```

### in wechaty
``` js
const payload = { "url": "" } // or payload = {"base64":"..."}
const api = await fetch('https://tosilk.zeabur.app/v1/encoder', payload)
const { data } = await api.json()
const silkBox = FileBox.fromBase64(data)
```