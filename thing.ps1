# Assume the current directory is where we want the new repository to be created
# Create the new repository
git init

# Before we do a merge, we have to have an initial commit, so we’ll make a dummy commit
dir > deleteme.txt
git add .
git commit -m `"Initial dummy commit`"

# Add a remote for and fetch the old repo
git remote add -f old_a https://github.com/kcool17/Arduino-Projects

# Merge the files from old_a/master into new/master
git merge old_a/master

# Clean up our dummy file because we don’t need it any more
git rm .\deleteme.txt
git commit -m `"Clean up initial file`"

# Move the old_a repo files and folders into a subdirectory so they don’t collide with the other repo coming later
mkdir old_a
dir -exclude old_a | %{git mv $_.Name old_a}

# Commit the move
git commit -m `"Move old_a files into subdir`"

# Do the same thing for old_b
git remote add -f old_b https://github.com/kcool17/python-games
git merge old_b/master
mkdir old_b
dir -exclude old_a,old_b | %{git mv $_.Name old_b}
git commit -m `"Move old_b files into subdir`"


# Do the same thing for old_c
git remote add -f old_c https://github.com/kcool17/Java-Programming-Class-Eclipse
git merge old_c/master
mkdir old_c
dir -exclude old_a,old_b,old_c | %{git mv $_.Name old_c}
git commit -m `"Move old_c files into subdir`"
