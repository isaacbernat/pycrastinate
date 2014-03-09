def execute_actions(config, data):
    #print "Found {} TODONES from {} developers at {}".format(total_unfiltered, len(data), os.getcwd())
    #print "These {} of them are older than {} and earlier than {} days:".format(total_filtered, config["earliest"], config["oldest"])
    for k, v in data.items():
        print k
        for l in v:
            print "  {}  {}  {}  {}  {}".format(l["token"], l["date"], l["line_count"], l["file_path"], l["code"])
