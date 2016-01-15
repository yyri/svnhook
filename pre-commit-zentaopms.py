import zentaopms, sys, os


if __name__ == "__main__":
    print sys.argv[1]
    jobinfo = str(sys.argv[1])
    idtype = jobinfo.split("#")[0]
    jobid = jobinfo.split("#")[1]
    comment = str(sys.argv[2])
    zentaopms.postzentao("comment", idtype, jobid, comment)
