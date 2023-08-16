#!/bin/bash
cd ./rt_option_menu/frontend
npm run build
cd ../../
python setup.py sdist bdist_wheel
# cp -r build/lib/rt_option_menu ~/miniconda3/envs/streamlit/lib/python3.8/site-packages
echo "Done :)"
