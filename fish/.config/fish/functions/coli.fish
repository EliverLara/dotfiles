function coli
  set -l last_status $status
  set -l cyan (set_color -o cyan)
  set -l yellow (set_color -o yellow)
  set -l red (set_color -o red)
  set -l blue (set_color -o blue)
  set -l green (set_color -o green)
  set -l normal (set_color normal)


      set arrow $yellow"⦿"


  set -l cwd $green(basename (prompt_pwd))



  echo -n -s $arrow ' ' $cwd  $normal ' '
end

