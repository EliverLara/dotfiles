function tabicon -d "Change current terminal title"
	set -l cyan (set_color -o cyan)
 	set -l normal (set_color normal) 
if [ (count $argv) -lt 1 ]
      echo "You need to specify a title to set"
      return 1
  end
	set t $argv

	switch $argv[1]
		case php
			set t " 🐘 "
		case python
			set t "  "
		case root
			set t " 🔥 💀 🔥  "
		case mysql 
			set t "  "
		case node 
			set t " "
		case ruby 
			set t "  "
		case electron
			set t "  "
		case git
			set t "   "
		case npm
			set t "   "
	


	end
  
	title $t
  #echo "function fish_title; echo  $t ; end" | source -
#	echo -n -s -e $cyan$t
end






































