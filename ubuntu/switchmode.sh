# --------------------------------- #
# Simple utility for switching between light and dark modes. Make sure the
# constants are set-up correctly to point to the correct (Alacritty) themes and
# Kvantum themes.
# Author: Kristian Ebstrup
# Email: kreb@dtu.dk
# --------------------------------- #
# Alacritty Config File
CONFIG_PATH="$HOME/.config/alacritty/alacritty.yml"

# Alacritty Light and Dark Themes
ALACRITTY_DARK="rose-pine-moon"
ALACRITTY_LIGHT="rose-pine-dawn"

# Kvantum Light and Dark Themes
KVANTUM_DARK="Fluent-roundDark"
KVANTUM_LIGHT="Fluent-round"

# Get current theme from Alacritty config yaml
current_theme=$(echo $(grep -Po 'colors/\K.*?(?=.yml)' $CONFIG_PATH))
echo "Current theme: $current_theme"
echo "Dark theme: $ALACRITTY_DARK"
echo "Light theme: $ALACRITTY_LIGHT"

# Match and set the opposite
case $current_theme in
    $ALACRITTY_DARK)
        echo "Detected dark mode. Switching to light."
        # Alacritty
        sed -i "s/${current_theme}/${ALACRITTY_LIGHT}/" $CONFIG_PATH 
        ;;
    $ALACRITTY_LIGHT)
        echo "Detected light mode. Switching to dark."
        # Alacritty
        sed -i "s/${current_theme}/${ALACRITTY_DARK}/" $CONFIG_PATH
        ;;
    *)
        echo "Unknown theme set in Alacritty. Resetting to Dark-mode"
        # Alacritty
        sed -i "s/${current_theme}/${ALACRITTY_DARK}/" $CONFIG_PATH
        ;;
esac
