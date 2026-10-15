-- Drop files or folders on this app to send them to homelab:~/Ferry.
on open theItems
	set args to ""
	repeat with f in theItems
		set args to args & " " & quoted form of POSIX path of f
	end repeat
	display notification ((count of theItems) as text) & " item(s), you will get a notice when they land" with title "Sending to homelab"
	try
		set out to do shell script "$HOME/.local/bin/ferry send" & args
		display notification (paragraph 1 of out) with title "Sent to homelab"
	on error errMsg
		display alert "ferry send failed" message errMsg as critical
	end try
end open

on run
	display dialog "Drag files or folders onto this icon to send them to homelab:~/Ferry." buttons {"OK"} default button 1
end run
