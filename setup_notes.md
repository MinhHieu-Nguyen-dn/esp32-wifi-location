1. Config env:  
`conda create -n iot_where python=3.5 -c conda-forge`  


2. Create a new PyCharm project with the above env (Conda env interpreter: Python 3.5 (iot_where)).  


3. Clone repo `whereami`:  
```
git clone https://github.com/kootenpv/whereami
cd whereami
```

4. Install dependencies:  
```
pip install -r requirements.txt
python setup.py install
```  

5. Setup project's structure:  
- Set content root to `whereami` folder (the outer folder the wraps this whole repo).  
- Mark directories in `.gitignore` as **Excluded**.   


6. Install `access_points` package (terminal in the wrapper folder `whereami`):  
`git clone https://github.com/kootenpv/access_points`  
Then mark the wrapper access_points folder (path is `.\whereami\access_points`) as **Sources root**.