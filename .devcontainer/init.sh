# Create file of export using the devcontainer-build.env

# Add prefix
awk '$0=" echo export "$0' devcontainer-build.env > buildenvscript_1.sh
# Add suffix
awk 'NF{print $0 " >> ~/.bashrc;"}' buildenvscript_1.sh > buildenvscript.sh
# Execute script
. ./buildenvscript.sh
