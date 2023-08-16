#!/usr/bin/env bash

#Needs curl and jq

check_command() {
  cmd="$1"
  msg="$2"

  if ! command -v "${cmd}" > /dev/null 2>&1; then
    echo "${cmd} is not available. Please install it. ${msg}";
    echo "Abort run."
    echo
    exit 1
  fi
}

check_command curl
check_command jq

if test $# -eq 0; then
	echo "This script needs a list of pages to download from the wiki"
	exit 1
fi
ALL_PAGES="$@"

echo "Please enter the user name and password to log on to Wiki"

echo -n "User: "
read USERNAME
echo
echo -n "Password: "
read -s USERPASS
echo
PAGE="Title of an article"
PREFIX_WIKI="https://www.aquila-consortium.org/wiki"
WIKIAPI="${PREFIX_WIKI}/api.php"
cookie_jar="wikicj"
#Will store file in wikifile

echo "UTF8 check: ☠"
#################login
echo "Logging into $WIKIAPI as $USERNAME..."

###############
#Login part 1
#printf "%s" "Logging in (1/2)..."
echo "Get login token..."
CR=$(curl -s -S \
	--location \
	--retry 2 \
	--retry-delay 5\
	--cookie $cookie_jar \
	--cookie-jar $cookie_jar \
	--user-agent "Curl Shell Script" \
	--keepalive-time 60 \
	--header "Accept-Language: en-us" \
	--header "Connection: keep-alive" \
	--compressed \
	--request "GET" "${WIKIAPI}?action=query&meta=tokens&type=login&format=json")

echo "$CR" | jq .

rm -f login.json
echo "$CR" > login.json
TOKEN=$(jq --raw-output '.query.tokens.logintoken' login.json)
TOKEN="${TOKEN//\"/}" #replace double quote by nothing

#Remove carriage return!
printf "%s" "$TOKEN" > token.txt
TOKEN=$(cat token.txt | sed 's/\r$//')


if [ "$TOKEN" == "null" ]; then
	echo "Getting a login token failed."
	exit
else
	echo "Login token is $TOKEN"
	echo "-----"
fi

###############
#Login part 2
echo "Logging in..."
CR=$(curl -s -S \
	--location \
	--cookie $cookie_jar \
    --cookie-jar $cookie_jar \
	--user-agent "Curl Shell Script" \
	--keepalive-time 60 \
	--header "Accept-Language: en-us" \
	--header "Connection: keep-alive" \
	--compressed \
	--data-urlencode "username=${USERNAME}" \
	--data-urlencode "password=${USERPASS}" \
	--data-urlencode "rememberMe=1" \
	--data-urlencode "logintoken=${TOKEN}" \
	--data-urlencode "loginreturnurl=http://www.aquila-consortium.org/wiki/" \
	--request "POST" "${WIKIAPI}?action=clientlogin&format=json")

echo "$CR" | jq .

STATUS=$(echo $CR | jq '.clientlogin.status')
if [[ $STATUS == *"PASS"* ]]; then
	echo "Successfully logged in as $USERNAME, STATUS is $STATUS."
	echo "-----"
else
	echo "Unable to login, is logintoken ${TOKEN} correct?"
	exit
fi


OUTFORMAT="rst"

download() {
  local d_title=$1
  local d_outfile=$2
  curl -s -S \
    --location \
    --cookie-jar wikicj \
    --cookie wikicj \
    "${PREFIX_WIKI}/index.php/${d_title}?action=raw" \
    | pandoc -f mediawiki -t ${OUTFORMAT} \
    | sed '/`.* <http.*>`/ { b }; s%`\(.*\) <\(.*\)>`%`\1 <\2.html>`%g'  > ${d_outfile}

 #The last command protects absolute URL but change relative links to html pages.
}

download_url() {
  local d_url="$1"
  local d_out="$2"
  echo "Downloading from $d_url..."
  curl -s -S \
    --location \
    --cookie-jar wikicj \
    --cookie wikicj \
    "$d_url" > ${d_out}
}

query_image() {
  local image=$1
  local result=$(curl -s -S \
    --location \
    --cookie-jar wikicj \
    --cookie wikicj \
    "${WIKIAPI}/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=File:${image}")
  
  r=$(echo "$result" | jq '.query.pages | keys[0]') 
  r2=$(echo "$result" | jq -r ".query.pages.${r}.imageinfo[0].url")
  echo $r2
  return 0
}

test -d download || mkdir download
for TITLE in ${ALL_PAGES}; do
  OUTFILE=download/${TITLE}.rst
  download ${TITLE} ${OUTFILE}
  grep '\.\. figure' ${OUTFILE} | awk -F ': ' '{ print $2; }' > image_list
  (while read; do
    url=$(query_image "$REPLY")
    download_url "${url}" "download/${REPLY}" 
  done) < image_list 
done

# ###############
# #Get edit token
# echo "Fetching edit token..."
# CR=$(curl -S \
# 	--location \
# 	--cookie $cookie_jar \
# 	--cookie-jar $cookie_jar \
# 	--user-agent "Curl Shell Script" \
# 	--keepalive-time 60 \
# 	--header "Accept-Language: en-us" \
# 	--header "Connection: keep-alive" \
# 	--compressed \
# 	--request "POST" "${WIKIAPI}?action=query&meta=tokens&format=json")
#
# echo "$CR" | jq .
# echo "$CR" > edittoken.json
# EDITTOKEN=$(jq --raw-output '.query.tokens.csrftoken' edittoken.json)
# rm edittoken.json
#
# EDITTOKEN="${EDITTOKEN//\"/}" #replace double quote by nothing
#
# #Remove carriage return!
# printf "%s" "$EDITTOKEN" > edittoken.txt
# EDITTOKEN=$(cat edittoken.txt | sed 's/\r$//')
#
# if [[ $EDITTOKEN == *"+\\"* ]]; then
# 	echo "Edit token is: $EDITTOKEN"
# else
# 	echo "Edit token not set."
# 	exit
# fi
#
# ###############
# #Make a test edit
# #EDITTOKEN="d55014d69f1a8c821073bb6724aced7658904018+\\"
# CR=$(curl -S \
# 	--location \
# 	--cookie $cookie_jar \
# 	--cookie-jar $cookie_jar \
# 	--user-agent "Curl Shell Script" \
# 	--keepalive-time 60 \
# 	--header "Accept-Language: en-us" \
# 	--header "Connection: keep-alive" \
# 	--compressed \
# 	--data-urlencode "title=${PAGE}" \
# 	--data-urlencode "appendtext={{nocat|2017|01|31}}" \
# 	--data-urlencode "token=${EDITTOKEN}" \
# 	--request "POST" "${WIKIAPI}?action=edit&format=json")
#
# echo "$CR" | jq .
