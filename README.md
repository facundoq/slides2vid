# slides2vid

Convert slides w/ notes to a video presentation using TTS.

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

    PDF-->ImagePreprocessor;
    PPTX-->ImagePreprocessor;
    ODT-->ImagePreprocessor;
    IF-->ImagePreprocessor;
    PPTX-->AudioPreprocessor;
    ODT-->AudioPreprocessor;
    AF-->AudioPreprocessor;
    TF-->AudioPreprocessor;
    
    subgraph ImagePreprocessor
        python-pptx
        uniconv
    end

    subgraph AudioPreprocessor
        python-pptx
        gTTS
        chatterbox-tts
    end

     subgraph SlideGenerator
        ffmpeg
    end

    ImagePreprocessor-->SIL[Slide Image List];
    AudioPreprocessor-->SAL[Slide Audio List];
    SAL-->SlideGenerator;
    SIL-->SlideGenerator;
    SlideGenerator-->Video;
    

```
