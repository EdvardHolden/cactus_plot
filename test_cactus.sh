
FILE=examples/cactus.png
python3 mkplot.py --legend prog_alias -t 1000 -b png --save-to examples/cactus.png examples/solver?.json
#python3 mkplot.py --legend prog_alias -t 1000 -b png --save-to examples/cactus.png --data_type db '{"117213": "1", "117214": "2"}' --db_data_ltb

if [ ! -f ""$FILE"" ]; then
    echo "ERROR"
    exit 1
fi
# Passing without issues
