FROM golang:1.17-alpine

WORKDIR /steintest

# Install dependencies
RUN apk add --no-cache iproute2

COPY . .

RUN go mod download

RUN go build -o client .

EXPOSE 8080
