FILE=examples/scatter.png
python3 mkplot.py -l -p scatter -b png --save-to examples/scatter.png --shape squared -t 1000 --y_log --y_max 10000 --y_min 0.1 --x_log examples/solver?.json

if [ ! -f ""$FILE"" ]; then
    echo "ERROR"
    exit 1
fi
# Passing without issues