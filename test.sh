#!/usr/bin/env bash
echo "Test to get non existing ID for child\n"
curl -X GET http://0.0.0.0:5000/api/v1/states/not_an_id/cities/

echo "Test to create new object\n"
echo "Create parent first\n"
curl -X POST http://0.0.0.0:5000/api/v1/states/ -H "Content-Type: application/json" -d '{"name": "First State"}' -vvv

echo "Wrong ID of new parent due to script issues\n"
curl -X POST http://0.0.0.0:5000/api/v1/states/0e590b04-9c02-4e93-9f1c-473f4a4fe0ce/cities -H "Content-Type: application/json" -d '{"name": "Alexandria"}' -vvv

echo "Let's print a real city with good id\n"
curl -X GET http://0.0.0.0:5000/api/v1/cities/a8cae264-b993-4d66-b68e-eeb4b1177401

echo "Let's edit it using PUT\n"
curl -X PUT http://0.0.0.0:5000/api/v1/cities/a8cae264-b993-4d66-b68e-eeb4b1177401 -H "Content-Type: application/json" -d '{"name": "Bossier City"}'

echo "Let's delete a city\n"
curl -X DELETE http://0.0.0.0:5000/api/v1/cities/a8cae264-b993-4d66-b68e-eeb4b1177401

echo "check if it was deleted\n"
curl -X GET http://0.0.0.0:5000/api/v1/states/a8cae264-b993-4d66-b68e-eeb4b1177401/cities/

