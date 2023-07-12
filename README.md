# tosilk

## Demo

You can try the `tosilk` service through the following link:
[https://tosilk.zeabur.app/docs](https://tosilk.zeabur.app/docs)


 
### Instructions
1. Obtain the base64 representation of your MP3 file. You can convert your MP3 file to base64 using various online tools or programming languages.
2. Replace `<your_mp3_base64>` or <your_mp3_url>  in the following commands with the actual base64 string of your MP3 file.

## Usage
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