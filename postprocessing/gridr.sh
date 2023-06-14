# ============================================ #
# Bash script for renaming all grid result files and mesh files
#
# Author: K. Ebstrup 
# Email: kreb@dtu.dk
# ============================================ #
read -p "Input string to replace 'grid': " replacer
for file in grid.*; do 
    mv "$file" "${file/grid/replacer}"
done
