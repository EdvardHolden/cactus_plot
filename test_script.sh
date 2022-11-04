
FILE=examples/cactus.png
python3 mkplot.py -l --legend prog_alias -t 1000 -b png --save-to examples/cactus.png examples/solver?.json

if [ ! -f ""$FILE"" ]; then
    echo "ERROR"
    exit 1
fi
# Passing without issues