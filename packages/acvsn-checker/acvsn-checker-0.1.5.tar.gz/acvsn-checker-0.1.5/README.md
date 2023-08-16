


<!-- PROJECT LOGO -->
<div align="center">

<h2 align="center">Atmospheric Composition Variable Standard Name Checker</h2>

  <p align="center">
    <br />
    <a href="https://github.com/ekqian/acvsn-checker"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/ekqian/acvsn-checker">View Demo</a>
    ·
    <a href="https://github.com/ekqian/acvsn-checker/issues">Report Bug</a>
    ·
    <a href="https://github.com/ekqian/acvsn-checker/issues">Request Feature</a>
    <br /><br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#installation">Installation</a></li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#check-name">Check Name</a></li>
        <li><a href="#check-file">Check File</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The ACVSN checker is a command line application that checks if a standard name meets the guidelines under the Atmospheric Composition Variable Standard Name Convention (ACVSNC). 

For complete documentation on ACVSNC, refer to [https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/acvsnc](https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/acvsnc). 



<!-- Installation -->
## Installation

To install the package onto your local device, run the following command in the terminal.

Make sure that Python version 3.4 or newer is installed.

   ```sh
   pip install
   ```


<!-- USAGE EXAMPLES -->
## Usage

The program has two main functionalities; it can check if a single standard name is valid and it can check if the standard names in an ICARTT (.ict) file are valid.

### Check Name
To check a standard name is valid, run the following command in the terminal:

```sh
checker check-name *standardname
   ```
*`*standardname
` is a user-inputted standard name.*

### Check File
To check the header of a file, run the following command in the terminal:

```sh
checker check-file *filepath
   ```
*`*filepath
` is the absolute path that points to the .ict file.*



<!-- LICENSE -->
## License

See `LICENSE.txt` for more information.



<!-- CONTACT -->
## Contact

Email: [ekqian@seas.upenn.edu](ekqian@seas.upenn.edu)

Github: [https://github.com/ekqian](https://github.com/ekqian)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
