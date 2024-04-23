# Mailingester

Extract information from emails.

# Development

This project requires Python 3.11+.

Clone the repository.
```
git clone https://github.com/IDEMSInternational/mailingester
cd mailingester
```

Create a Python venv.
```
python -m venv .venv
```

Activate the venv.
```
# Linux and MacOS
source .venv/bin/activate

# Windows - cmd.exe
.venv\Scripts\activate.bat

#Windows - PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies.
```
pip install -e '.[dev]'
```

Run tests.
```
pytest
```

Run server.
```
python -m aiosmtpd -u -n -c mailingester.handlers.MailServer config.json
```

# Configuration

The server is configured via a JSON file. See [config.json] for an example. The available settings are listed below.

- `mail_dir`: local file system path where the inbox is located
- `storage`: storage system where extracted information will be stored
- `extractors`: list of extractors that will be used to extract information from emails

## Storage

The storage key is an object with two keys.

- `name`: Python class of the storage system to use; there are two built-in options, `mailingester.storage.LocalFileSystem` and `mailingester.storage.GoogleCloudStorage`.
- `args`: object containing keyword arguments to pass to the constructor of the storage class

### LocalFileStorage

Contructor arguments:

- `root`: directory to consider as the root, under which all files will be stored

### GoogleCloudStorage

Contructor arguments:

- `bucket`: name of storage bucket where files will be stored

## Extractors

The extractors key is a list of objects that define the extractors to use. Each extractor is defined by an object with two keys.

- `name`: Python class of the extractor; there is one built-in, `mailingester.extractors.ZambiaExtractor`
- `args`: object containing keyword arguments to pass to the constructor of the extractor class

### ZambiaExtractor

Contructor arguments:

- `allowed`: list of sender email addresses - a match of any with the sender of an email will indicate that this extractor should be used


[config.json]: config.json
