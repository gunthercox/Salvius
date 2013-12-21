printf "Moving files into current directory...\n"

sudo mv -f * ./Salvius/[A-Za-z0-9]* ../

printf "Removing empty download directory"

sudo rm -r Salvius

printf "Giving permissions to current user"

sudo chown $USER -R ../www

printf "Updating package cache...\n"

sudo apt-get update

printf "Installing non-required packages\n"

sudo apt-get install nginx git make
