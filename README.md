

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Shulammiteya/Tone-Helper-Backend">
    <img src="https://drive.google.com/uc?export=view&id=1AQ0-e869kWLbsq3zFLe61IvGrQvTrFPW" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Tone Helper (backend)</h3>

  <p align="center">
    Backend of speech synthesis application.
    <br />
    <a href="https://github.com/Shulammiteya/Tone-Helper-Backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://youtu.be/JIWPWQkKXA4">View Demo</a>
    ·
    <a href="https://github.com/Shulammiteya/Tone-Helper-Backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/Shulammiteya/Tone-Helper-Backend/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#api-discription">API Discription</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
<br />
</details>



<!-- ABOUT -->
## About

The back-end server for speech synthesis applications, [Tone Helper](https://github.com/Shulammiteya/Tone-Helper-Frontend).

With the API provided by the server, you can do:
* **speech recognition**
* **pitch detection**
* **file conversion**
* **speech synthesis**

Of course, since your needs may be different, you are very welcome to suggest changes by forking this repo and creating a pull request or opening an issue!
<br />
<br />



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.7
* HTTPS Server

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Shulammiteya/Tone-Helper-Backend.git
   ```
2. Install libraries
   ```sh
    pip3 install pydub SoundFile pyworld google-cloud-core
   ```
4. Create your own credential file in the root directory
   ```sh
   touch ./sample.json
   ```

5. Run the server
   ```sh
    python3 backend.py
   ```
   
<br />


<!-- API discription -->
## API Discription

#### 
  |   API     |   stt   |   tune  |   getURL  |
  |   -       |   -     |   -     |   -       |
  |   Method  |   POST  |   POST  |   GET    |
####

---
#### /stt	
<details>
<Summary>  input： </Summary>	       
<table>
    <thead>
        <th>Key</th>
        <th>Type</th>
        <th>Value</th>
        <th>Description</th>
    </thead>
    <tr>
        <td rowspan="1">audio</td>
        <td>audio/m4a</td>
        <td></td>
        <td>Audio files for speech recognition, pitch detection, and transcoding</td>
    </tr>
</table>
</details>

<details>
<Summary>  output： </Summary>	
<table>
    <thead>
        <th>Key</th>
        <th>Type</th>
        <th>Value</th>
        <th>Description</th>
    </thead>
    <tr>
        <td>audio</td>
        <td>base64</td>
        <td>...BwbGVhc3VyZS4=</td>
        <td>WAV file encoded in base64</td>
    </tr>
    <tr>
        <td>wordInfo</td>
        <td>array</td>
        <td>
          [<br>
             {   <br>
                "word": "一",   <br>
                "start": 27002,   <br>
                "end": 98000,   <br>
                "f0": 440.15,   <br>
                "f0Start": 54,   <br>
                "f0End": 196   <br>
             },   <br>
             {   <br>
                ...   <br>
             },   <br>
             ...   <br>
          ]<br>
        </td>
        <td>
          "word": the Speech-recognized text   <br>
          "start": the starting position in the audio array   <br>
          "end": the end position in the audio array   <br>
          "f0": the average F0   <br>
          "f0Start": the starting position in the f0 array   <br>
          "f0End": the end position in the f0 array
        </td>
    </tr>
</table>
</details>

---
#### /tune	
<details>
<Summary>  input： </Summary>	       
<table>
    <thead>
        <th>Key</th>
        <th>Type</th>
        <th>Value</th>
        <th>Description</th>
    </thead>
    <tr>
        <td rowspan="1">audio</td>
        <td>audio/wav</td>
        <td></td>
        <td>Audio file to be tuned</td>
    </tr>
    <tr>
        <td>f0</td>
        <td>JSON</td>
        <td>
          {<br>
             659.26,   <br>
             659.26,   <br>
             440.00,   <br>
             ...   <br>
          }<br>
        </td>
        <td>Designated F0</td>
    </tr>
</table>
</details>

<details>
<Summary>  output： </Summary>	
<table>
    <thead>
        <th>Key</th>
        <th>Type</th>
        <th>Value</th>
        <th>Description</th>
    </thead>
    <tr>
        <td rowspan="3">data</td>
        <td rowspan="3">base64</td>
        <td>...BwbGVhc3VyZS4=</td>
        <td>Synthesized audio encoded in base64</td>
    </tr>
</table>
</details>

---
#### /getURL	
<details>
<Summary>  output： </Summary>	       
<table>
    <thead>
        <th>Key</th>
        <th>Type</th>
        <th>Value</th>
        <th>Description</th>
    </thead>
    <tr>
        <td rowspan="1">data</td>
        <td>string</td>
        <td>https://youtu.be/...</td>
        <td>Introductory video URL</td>
    </tr>
</table>
</details>

<br />



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<br />



<!-- CONTACT -->
## Contact

About me: [Hsin-Hsin, Chen](https://www.facebook.com/profile.php?id=100004017297228) - shulammite302332@gmail.com

Project Link: [https://github.com/Shulammiteya/Tone-Helper-Backend](https://github.com/Shulammiteya/Tone-Helper-Backend)


