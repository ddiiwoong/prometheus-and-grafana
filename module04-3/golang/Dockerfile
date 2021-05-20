FROM golang:1.16.0 as builder

# Set the Current Working Directory inside the container
WORKDIR /app

RUN export GO111MODULE=on

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags '-s -w' -o main .

FROM scratch
COPY --from=builder /app /

# Expose port 9001 to the outside world
EXPOSE 9001

# Command to run the executable
CMD ["./main"]