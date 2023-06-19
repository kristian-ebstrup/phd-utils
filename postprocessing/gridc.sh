
# ============================================ #
# Bash script for cleaning all grid results files (i.e. keeping grid.X?D and
# grid.T?D) to prepare a clean run.
#
# Author: K. Ebstrup 
# Email: kreb@dtu.dk
# ============================================ #
echo "Warning! You are about to delete your EllipSys result files!"
read -p "==> PLEASE CONFIRM [y/N]: " yes_or_no
yes_or_no=${yes_or_no:-n}
if [ ${yes_or_no,,} == "y" ] 
then
    echo "Deleting grid.?force ..."
    rm grid.?force
    echo "Deleting grid.?pr ..."
    rm grid.?pr
    echo "Deleting grid.OUT ..."
    rm grid.OUT
    echo "Deleting grid.res ..."
    rm grid.res
    echo "Deleting grid.RST.0? ..."
    rm grid.RST.0?
    echo "Done"
else
    echo "Cancelled deletion."
fi
