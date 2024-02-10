function pack \
    --description="Fish-shell colorful ASCII-art logo" \
    --argument-names _theme variant

	# defaults:
    [ $_theme  ]; or help_usage
    [ $variant ]; or help_usage

	set -l variants master standard-buttons slim slim-standard-buttons alt-style
	set -l folders xfwm4 metacity-1 gtk-4.0 gtk-3.20 gtk-3.0 gtk-2.0 gnome-shell unity assets cinnamon

	if test $_theme != "all"
		set target $_theme 
	else
		set target Ant Dracula Bloody Nebula
	end

	if test $variant != "all"
		set variant $variant
	else
		set variant $variants
	end

	echo packaging $target $variant

	for i in $target;
	#	set current Ant
		if test $i != "Ant"
			set  current Ant-$i
		else
			set current Ant
		end

		#Go to root theme folder on github
		cd $current

		for v in $variant;
			#echo "verga"
			#set current $current-$v

			echo checking out to $v
			git checkout -q $v

			git push

			echo Copying $current files
			mkdir -p ../gnome-look/$current
			for f in $folders;
				cp -r $f ../gnome-look/$current
			end;
			cp index.theme README.md LICENSE ../gnome-look/$current
			

			#Go to root theme folder on gnome-look
			cd ../gnome-look/$current

			echo "Deleting unecessary files to $current"
			rm xfwm4/render_assets.fish
			rm -rf xfwm4/assets gtk-3.20/assets

			# back to gnome-look folder
			cd ..

			echo "Compressing $current"
			if test $v != "master"
				tar -cf $current-$v.tar.xz $current/* --xz
			else
				tar -cf $current.tar.xz $current/* --xz
			end

			rm -rf $current

			#back to root theme folder on github
			cd ../$current

		;end

		#back to github folder
		cd ..

		#Create slim file
		tar -cf gnome-look/$current-Slim.tar -C gnome-look $current-slim.tar $current-slim-standard-buttons.tar --xz
		rm gnome-look/$current-slim.tar gnome-look/$current-slim-standard-buttons.tar
		# # $variant == 0 -> mac style buttons
		# if test $variant -eq 1
		# 	git checkout standard-buttons
		# else if test $variant -eq 0
		# 	git checkout master
		# else if test $variant -eq 2
		# 	git checkout slim-standard-buttons
		# else if test $variant -eq 4
		# 	git checkout alt-style
		# else
		# 	git checkout slim
		# end

		# echo "Deleting unecessary files to $current"
		# rm Gulpfile.js *.json .gitignore xfwm4/render_assets.fish
		# rm -rf .git .sass-cache node_modules xfwm4/assets gtk-3.20/assets
		
		# cd ..

		# echo "Compressing $current"
		# if test $variant -eq 0
		# 	tar -cf $current.tar $current/* --xz
		# else if test $variant -eq 1
		# 	tar -cf $current-standard-buttons.tar $current/* --xz

		# else if test $variant -eq 2
		# 	tar -cf $current-slim-standard-buttons.tar $current/* --xz
		# else if test $variant -eq 4
		# 	tar -cf $current-alternative-style.tar $current/* --xz
		# else
		# 	tar -cf $current-slim.tar $current/* --xz
		# end
		
		# cd ..
	;end

end
