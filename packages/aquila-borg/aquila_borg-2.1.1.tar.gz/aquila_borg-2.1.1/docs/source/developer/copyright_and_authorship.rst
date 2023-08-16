Copyright and authorship
========================

ARES/BORG is developed under CECIL/v2.1 license, which is compatible
with the GNU Public License (GPL). The GPL is fundamentally based on
Anglo-Saxon law and is not fully compatible with European laws. However
CECIL implies GPL protections and it is available in at least two
European languages, French and English. Keep in mind that in principle
your moral rights on the software that you write is your sole ownership,
while the exploitation rights may belong to the entity which has paid
your salary/equipment during the development phase. An interesting
discussion on French/European author protection is given
`here <http://isidora.cnrs.fr/IMG/pdf/2014-07-07_-_Droit_d_auteur_des_chercheurs_Logiciels_Bases_de_Donne_es_et_Archives_Ouvertes_-_Grenoble_ssc.pdf>`__
(unfortunately only in French, if anybody finds an equivalent in English
please post it here).

How to specify copyright info in source code ?
----------------------------------------------

As the main author of the code is becoming diverse it is important to
mark fairly who is/are the main author(s) of a specific part of the
code. The current situation is the following:

-  if an "ARES TAG" is found in the source code, it is used to fill up
   copyright information. For example

.. code:: c++

   // ARES TAG: authors_num = 2
   // ARES TAG: name(0) = Guilhem Lavaux
   // ARES TAG: email(0) = guilhem.lavaux@iap.fr
   // ARES TAG: year(0) = 2014-2018
   // ARES TAG: name(1) = Jens Jasche
   // ARES TAG: email(1) = jens.jasche@fysik.su.se
   // ARES TAG: year(1) = 2009-2018

this indicates that two authors are principal authors, with their name,
email and year of writing.

-  In addition to the principal authors, minor modifications are noted
   by the script and additional names/emails are put in the 'Additional
   Contributions' sections
-  by default Guilhem Lavaux and Jens Jasche are marked as the main
   authors. When all the files are marked correctly this default will
   disappear and an error will be raised when no tag is found.
