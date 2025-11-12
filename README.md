# slides2vid

Convert slides w/ notes to a video presentation using TTS.

Supported input formats:

* Slide images
  * PDF
  * ODT
  * Image Folder
* Slide audio
  * ODT
  * PPTX
  * Audio Folder

Supported output formats:
* Video (MKV/M4a)
* Subtitules (planned)
* HTML/JS (planned)


Supported TTS Engines:
* gTTS
* ChatterboxTTS

```mermaid
 flowchart-elk LR;
   
flowchart-elk LR;
    PDF{{📄 PDF}}
    PPTX{{📄 PPTX}}
    ODT{{📄 ODT}}
    AF{{🖿🎤 Audio Folder}}
    TF{{🖿💬 Text Folder}}
    IF{{🖿🖼️ Image Folder}}
    Video{{🎥 Video}}

    PDF-->ImageConverter;
    PPTX-->ImageConverter;
    ODT-->ImageConverter;
    IF-->ImageConverter;
    PPTX-->AudioConverter;
    ODT-->AudioConverter;
    AF-->AudioConverter;
    TF-->AudioConverter;
    
    subgraph ImageConverter
        python-pptx
        uniconv
    end

    subgraph AudioConverter
        python-pptx
        gTTS
        chatterbox-tts
    end

     subgraph SlideGenerator
        ffmpeg
    end

    ImageConverter-->SIL[Slide Image List];
    AudioConverter-->SAL[Slide Audio List];
    SAL-->SlideGenerator;
    SIL-->SlideGenerator;
    SlideGenerator-->Video;
```
