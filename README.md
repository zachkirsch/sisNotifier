# sisNotifier

This is a program for Tufts CS students to use to get updated when grades are
posted on SIS.

#### Step 1: ssh into the homework server

    ssh UTLN@homework.cs.tufts.edu

#### Step 2: Clone this repository

    git clone https://github.com/zachkirsch/sisNotifier.git && cd sisNotifier

#### Step 3: Run the setup script

    sh setup

If you get some "Disk Quota Exceeded" errors, you don't have enough space for
all the dependencies. This requires about 75 megabytes of space.

#### Step 4: Create password file

__The next few paragraphs are important. Only use this program is you feel
comfortable doing so.__

In order to access SIS on your behalf, it needs your SIS password. To achieve
this, you will need to place your SIS password in a file (for example, in the
`sisNotifier` directory in a file called `password.txt`). Your SIS password is
your Tufts password, not your Tufts CS password.

Of course, you should make sure not to share this file with anyone, or grant
permissions to this directory to anybody else.

`password.txt` is included in the `.gitignore` for this repository, but if you
name your password file something else, you should add that filename to the
`.gitignore`.

Your password is never used as an argument to a script, so would-be sleuths who
inspect server processes will not be able to see your password. However, the
_filename_ of your password file is passed as an argument, and is thus visible
to other users.

The only script that accesses your password is `parseGrades.py`, which uses
your password to sign onto SIS.

    vim password.txt
    <enter SIS password>
    <realize you weren't in insert mode, so now everything is screwed up>
    <press I for insert mode>
    <enter SIS password>
    <spend 10 minutes trying to figure out how to exit Vim>
    <Escape>
    <:x>
    <phew>

#### Step 5: Try it

You can test if the script works by running `notifer.sh`:

    sh notify.sh <SIS username> <password file> <email>

For example, if your name is Jane Smith and your password is stored in
`password.txt`, run the following command:

    sh notify.sh jsmith01 password.txt jane.smith@tufts.edu

It should print out your grades to the terminal.

#### Step 6: Run daemon

Everything is now set up! With the included `daemon.sh`, you can run the
notifier script repeatedly.

    sh daemon.sh <epoch expiration> sh notify.sh <SIS username> <password-file> <email>

Combined with `nohup`, you can set the notifier to run in the background after
you log off.

For the notifier to expire on 1/5/2017 (after grades are due), use the
expiration 1483574400.

So, as an example, if your name is Jane Smith and your password is stored in
`passsword.txt`, run the following command:

    nohup sh daemon.sh 1483574400 sh notify.sh jsmith01 password.txt jane.smith@tufts.edu > /dev/null &

#### Step 6: Logout

You can now logout of the homework server, and you'll get an email every time
your grades are updated on SIS.

    logout


## About

Created by Zach Kirsch, December 2016

Feel free to let me know if there are any problems.

