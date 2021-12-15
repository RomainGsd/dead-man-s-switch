# Dead man's switch
A switch that is designed to be activated or deactivated if the human operator becomes incapacitated.

## What is my purpose

As said on [deadman.io](http://www.deadman.io/):

*Deadman is a service that will contact you by phone, email, or text-message to make sure everything is OK. If you don't respond, Deadman will email, call, or text any number of people that you define and send them documents, photos, or any other electronic file.*

## Instructions
### Credentials file
You must have a file named *credentials* at the root of the server.

You can find an explanation in *credentials_howto* and an example in *credentials*.

### Build the docker image
> docker build -t dms .
>
> docker run -d dms