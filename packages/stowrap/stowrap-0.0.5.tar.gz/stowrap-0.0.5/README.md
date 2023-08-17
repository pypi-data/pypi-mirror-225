# stowrap
Python Storage Service Wrapper

## How to use
### Initialize client
```
import stowrap

c = stowrap.Client("gcs")

or

c = stowrap.Client("s3")

```

### Upload a file
```
result = c.upload("my-bucket", "/path/to/local/file", "dstfile.txt")
print(result.url)
```
