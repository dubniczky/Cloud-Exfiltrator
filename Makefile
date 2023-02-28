data_dir = "data"

# Clean up the exfiltrated data directory
clean::
	@rm -rf $(data_dir)
	@mkdir $(data_dir)
