function change-theme \
    --description="Fish-shell colorful ASCII-art logo" \
    --argument-names _type value 

    # defaults:
    [ $_type  ]; or help_usage
    [ $value ]; or help_usage

    switch $_type
	        case "gtk"
	            gsettings set org.gnome.desktop.interface gtk-theme $value
				ln -sf ~/github/$value/gtk-4.0/gtk.css ~/.config/gtk-4.0/
				ln -sf ~/github/$value/assets/ ~/.config/
	        case "icon"
	            gsettings set org.gnome.desktop.interface icon-theme $value
	        case "shell"
	            gsettings set org.gnome.shell.extensions.user-theme name $value
	        case "cinnamon"
	            gsettings set org.cinnamon.desktop.interface gtk-theme $value
				gsettings set org.cinnamon.desktop.wm.preferences theme $value
				gsettings set org.cinnamon.theme name $value
	end

end

function help_usage
	echo "change-theme usage: change-theme [gtk | shell | icon] value"
end
