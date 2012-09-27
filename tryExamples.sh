EXAMPLE_ROOT=~/Amiga/disks/AMOSPro_Examples/Examples
for path in ${EXAMPLE_ROOT}/H-*; do
    for file in ${path}/*.AMOS; do
        if ! python amosToText.py "${file}" >/dev/null; then
            echo "Unfound tokens or problems in file $file"
        fi
    done
done
