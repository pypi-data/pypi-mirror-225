import io
from jag_util import int_to_chunksize

DOCTYPE_HTML = b'<!DOCTYPE HTML>'


class _target:
	def __init__(self, tgt=None):
		self.is_buf = True
		if not tgt:
			self.buf = io.BytesIO()
			self.write = self.buf.write
		else:
			self.is_buf = False
			self.write = tgt.sendall




class html_stream:
	"""
	Progressively generate and stream an html document.
	Create the document like so:
	doc = html_stream(con, doctitle='Pootis')
	con is an open connection with the client.
		The headers should be already flushed and Encoding-Type set to "chunked"
	"""
	def __init__(self, tgt_con=None, doctitle='Jag'):
		self.target = _target(tgt_con)

		# send the opening of the document
		doc_open = DOCTYPE_HTML + b'\n' + b'<html>'
		self.send(doc_open)


	def etag(self, tgname, attrs=None, sc=False, text=None, _parent=None):
		return etag(tgname, attrs, sc, text, self)


	def send(self, data):
		if self.target.is_buf:
			self.target.write(data)
		else:
			# send the chunk size
			self.con.sendall(int_to_chunksize(len(data)))
			# send the chunk itself
			self.con.sendall(data)
			# send separator
			self.con.sendall(b'\r\n')



class etag:
	"""
	Simple representation of an HTML tag.
	Open it using "with" statement, like so:
	with etag('img', attrs=[('class', 'pootis')], sc=True) as tag:
		print(tag.opening)
	"""
	def __init__(self, tgname, attrs=None, sc=False, text=None, _parent=None):
		if _parent:
			self.target = _parent.target
		else:
			self.target = _target()

		self.buf = io.BytesIO(f'<{tgname} '.encode())

		# self closing
		self.sc = sc

		self.tgname = tgname

		# append attributes
		if attrs:
			for at_name, at_val in attrs:
				if at_val:
					self.buf.write(f'{at_name}="{str(at_val).replace('"', r'\"')}" '.encode())
					continue

				self.buf.write(str(at_name).encode())

		# close the opening
		self.buf.write(b'/>' if sc else b'>')

		# Write opening to the main buffer
		self.target.write(self.buf.getvalue())

		# send text to the main buffer, if any
		if text and not sc:
			if isinstance(text, bytes)
				self.target.write(text)
			else:
				self.target.write(str(text).encode())

		# flush temp buffer
		self.buf = None

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		# If it's not a self-closing tag - close it
		if not self.sc:
			self.target.write(f'</{self.tgname}>'.encode())

	def etag(self, tgname, attrs=None, sc=False, text=None, _parent=None):
		return etag(tgname, attrs, sc, text, self)













