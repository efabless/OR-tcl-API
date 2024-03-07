package require fileutil

namespace eval sta {
    array set cmd_args {}
    array set hidden_cmd_args {}
    proc define_cmd_args { cmd arglist } {
      variable cmd_args

      set cmd_args($cmd) $arglist
    }
    proc define_hidden_cmd_args { cmd arglist } {
      variable hidden_cmd_args

      set hidden_cmd_args($cmd) $arglist
    }

    proc proc_redirect { proc_name body } {
      set proc_body [concat "proc $proc_name { args } {" \
               "global errorCode errorInfo;" \
               "set redirect \[parse_redirect_args args\];" \
               "set code \[catch {" $body "} ret \];" \
               "if {\$redirect} { redirect_file_end };" \
               "if {\$code == 1} {return -code \$code -errorcode \$errorCode -errorinfo \$errorInfo \$ret} else {return \$ret} }" ]
      eval $proc_body
    }
}

if { $argc != 2 } { 
    puts "Wrong number of args"
    puts "File required"
    puts "Directory required"
    exit 1
}
set out_dir [lindex $argv 1]
set input_files [fileutil::cat [lindex $argv 0]]
array unset sta::cmd_args *
foreach input_file $input_files {
    if { $input_file eq "" } {
        continue
    }

    set fbasename [file rootname [file tail $input_file]]

    source $input_file
    exec mkdir -p $out_dir
    exec mkdir -p $out_dir/$fbasename
    foreach {command description} [array get sta::cmd_args] {
        set output_file $out_dir/$fbasename/$command
        set out_stream [open $output_file w+]
        regsub -all {\[} $description {\1} description_pretty
        regsub -all {\]} $description_pretty {\1} description_pretty
        puts "Generting $output_file"
        foreach item [split $description_pretty "-"] {
            if { $item ne "" && $item ne " " } {
                puts $out_stream -$item
            }
        }
        close $out_stream
    }
    array unset sta::cmd_args *
}
