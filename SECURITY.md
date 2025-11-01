# Security Policy for PQChub

## Supported Versions
- Only the latest major and minor releases are actively supported.

## Reporting a Vulnerability
If you discover a security vulnerability in PQChub:

1. **Do not open a public issue.**
2. **Email details to:** security@qudslab.org
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Impact assessment
   - Potential fixes or mitigations
   - Platform and version details

## Disclosure Process
- The maintainers will acknowledge receipt within 2 business days.
- Investigation and remediation will begin immediately.
- You will be kept informed of progress and resolution.
- A public advisory will be issued after a fix is released.

## Security Best Practices
- All cryptographic operations use vetted PQClean implementations.
- Memory is cleared after use where possible.
- Constant-time operations are used for sensitive data.
- Platform-specific mitigations are applied as needed.

## External Audits
- PQChub welcomes independent security audits.
- Please contact security@qudslab.org for coordination.

## References
- [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [PQClean Project](https://github.com/PQClean/PQClean)

---

For general questions, use GitHub Discussions. For urgent security issues, use the email above.