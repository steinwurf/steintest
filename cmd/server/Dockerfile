FROM golang:1.17-alpine

WORKDIR /steintest

COPY . .

RUN go mod download

RUN go build -o server .

EXPOSE 8080

CMD ["./server", "-serverParams", "serverParams.json"]