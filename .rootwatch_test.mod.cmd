savedcmd_rootwatch_test.mod := printf '%s\n'   rootwatch_test.o | awk '!x[$$0]++ { print("./"$$0) }' > rootwatch_test.mod
