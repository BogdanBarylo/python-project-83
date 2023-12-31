[![Actions Status](https://github.com/BogdanBarylo/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/BogdanBarylo/python-project-83/actions)
[![Python CI](https://github.com/BogdanBarylo/python-project-83/actions/workflows/github_actions.yml/badge.svg)](https://github.com/BogdanBarylo/python-project-83/actions/workflows/github_actions.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b94b15148d150a5a74f/maintainability)](https://codeclimate.com/github/BogdanBarylo/python-project-83/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7b94b15148d150a5a74f/test_coverage)](https://codeclimate.com/github/BogdanBarylo/python-project-83/test_coverage)

## Page Analyzer is a website that analyzes specified pages for SEO suitability

### View site here:

[Page Analyzer](https://page-analyzer-rrig.onrender.com)

[Here you can see how it works](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImI2MTIyN2RlOTgwMDY1NGZmMjU2M2IyNGIzMTA0YWMyLmdpZiIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=d7e38ccd6085c1197b7b6fa6e3ec1ccefe24d8565fe6d5983ac43e026103b898)
 
## Usage

1. Enter a URL in the input field and click "Проверить" button
3. On the url page click "Запустить проверку" button to start check
4. See the result below
5. Navigate to the "Сайты" page to see a list of all analyzed URLs
6. Click on a URL to view its detailed analysis history


## Installation requirements

- Python: 3.10
- Poetry: 1.4.0


#### Repository cloning
```bash
git clone git@github.com:BogdanBarylo/python-project-83.git
cd python-project-83
```


#### Create Database

```bash
whoami
{username}
sudo -u postgres createuser --createdb {username} 
createdb {databasename}
psql {databasename}
```



#### Secret Key

```bash
Create a file for environment variables in the page_analyzer .env directory with the following information
DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{databasename}  
SECRET_KEY='{your secret key}'
```


#### Installing dependencies

```bash
make install
```


#### Local use

```bash
make dev
```


#### Deploy

```bash
make build    
make start
```

## Contributions

Contributions to the Page Analyzer project are always welcome! If you encounter any issues or have suggestions for enhancements, please submit an issue or pull request. 