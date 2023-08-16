.. _development_with_git:

Development with git
====================

In case you are not familiar with the git version control system please
also consult the corresponding tutorial on git for bitbucket/atlassian
`here <https://www.atlassian.com/git/tutorials/what-is-version-control>`__.

In the following we will assume that your working branch is called
"my_branch". In addition the "master" branch should reflect the "master"
of the "blss" repository (the reference repository). Further in the
following we will consider the ARES main infrastructure here.

.. note::
   :code:`get-aquila-modules.sh` sets up git hooks to verify the quality of the code
   that is committed to the repository. It relies in particular on :code:`clang-format`. On GNU/Linux system,
   you may download static binaries of clang-format `here <https://aur.archlinux.org/packages/clang-format-static-bin/>`__.


Slides of the tutorial
----------------------

See `this file <https://www.aquila-consortium.org/wiki/index.php/File:ARES_git.pdf>`__.

Finding the current working branch
----------------------------------

.. code:: bash

   git branch

Branching (and creating a new branch) from current branch
---------------------------------------------------------

.. code:: bash

   git checkout -b new_branch

This will create a branch from current state move to the new branch
"new_branch"

Setting up remote
-----------------

First we add the remote:

.. code:: bash

   git remote add blss git@bitbucket.org:bayesian_lss_team/ares.git

Next we can fetch:

.. code:: bash

   git fetch blss

Pulling updates
---------------

Be sure that you are in the master branch

.. code:: bash

   git checkout master

Pull any updates from blss

.. code:: bash

   git pull blss master

Here you may get merge problem due to submodules if you have touched the
.gitmodules of your master branch. In that case you should revert the
.gitmodules to its pristine status:

.. code:: bash

   git checkout blss/master -- .gitmodules

This line has checked out the file .gitmodules from the blss/master
branch and has overwritten the current file.

And then do a submodule sync:

.. code:: bash

   git submodule sync

And an update:

.. code:: bash

   git submodule update

Now your master branch is up to date with blss. You can push it to
bitbucket:

.. code:: bash

   git push

This will update the master branch of *your fork* on bitbucket. Now you
can move to your private branch (e.g. "my_branch").

Rebase option for adjusting
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rebasing is better if you intend to create a pull request for the
feature branch to the master. That ensures that no spurious patch will
be present coming from the main branch which would create a merge
conflict.

Now you can rebase your branch on the new master using:

.. code:: bash

   git rebase master 

Merging option
~~~~~~~~~~~~~~

If you want to merge between two branches (again you should not merge
from master to avoid polluting with extra commits):

.. code:: bash

   git merge other_branch

Pushing modifications, procedures for pull requests
---------------------------------------------------

Cherry picking
~~~~~~~~~~~~~~

It is possible to cherry pick commits in a git branch. Use "git
cherry-pick COMMIT_ID" to import the given commit to the current branch.
The patch is applied and directly available for a push.

Procedure for a pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes the procedure of how to create your own developer
branch from the ARES master repository. Go to the master branch (which
should reflect BLSS master branch):

.. code:: bash

   git checkout blss/master

Create a branch (e.g. 'your_branch') with:

.. code:: bash

   git checkout -b your_branch

Import commits, either with git merge:

.. code:: bash

   git merge your_branch

or with cherry-picking:

.. code:: bash

   git cherry-pick this_good_commit
   git cherry-pick this_other_commit

where this_good_commit and this_other_commit refer to the actual commits
that you want to pick from the repository

Push the branch:

.. code:: bash

   git push origin your_branch

and create the pull request.

Please avoid at maximum to contaminate the pull request with the
specificity of your own workspace (e.g. gitmodules update etc).

Using tags
----------

To add a tag locally and push it:

.. code:: bash

   git tag <tagname>
   git push --tags

To delete a local tag:

.. code:: bash

   git tag --delete >tagname>

To delete a remote tag:

.. code:: bash

   git push --delete <remote> <tagname>

or

.. code:: bash

   git push <remote> :<tagname>

Reference [1]_.

.. _archivingrestoring_a_branch:

Archiving/restoring a branch
----------------------------

The proper way to do archive a branch is to use tags. If you delete the
branch after you have tagged it then you've effectively kept the branch
around but it won't clutter your branch list. If you need to go back to
the branch just check out the tag. It will effectively restore the
branch from the tag.

To archive and delete the branch:

.. code:: bash

   git tag archive/<branchname> <branchname>
   git branch -D <branchname>

To restore the branch some time later:

.. code:: bash

   git checkout -b <branchname> archive/<branchname>

The history of the branch will be preserved exactly as it was when you
tagged it. Reference [2]_.

.. [1]
   https://stackoverflow.com/questions/5480258/how-to-delete-a-remote-tag

.. [2]
   https://stackoverflow.com/questions/1307114/how-can-i-archive-git-branches
