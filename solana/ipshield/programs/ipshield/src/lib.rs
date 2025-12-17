use anchor_lang::prelude::*;
use anchor_lang::solana_program::clock;

declare_id!("GsXiSpv8sdArgivKGfDSRcTkZSNXGWqYnVjD758CgApg");

#[program]
pub mod ipshield {
    use super::*;

    /// Register new content
    pub fn register_content(
        ctx: Context<RegisterContent>,
        content_hash: String,
        ipfs_url: String,
    ) -> Result<()> {
        let registry = &mut ctx.accounts.content_registry;

        // Prevent duplicate registration
        require!(
            registry.timestamp == 0,
            ErrorCode::ContentAlreadyRegistered
        );

        registry.owner = *ctx.accounts.user.key;
        registry.content_hash = content_hash;
        registry.ipfs_url = ipfs_url;
        registry.timestamp = clock::Clock::get()?.unix_timestamp;

        Ok(())
    }

    /// Submit an infringement report
    pub fn report_infringement(
        ctx: Context<ReportInfringement>,
        original_hash: String,
        infringing_url: String,
    ) -> Result<()> {
        let report = &mut ctx.accounts.infringement_report;

        report.original_hash = original_hash;
        report.infringing_url = infringing_url;
        report.reporter = *ctx.accounts.reporter.key;
        report.timestamp = clock::Clock::get()?.unix_timestamp;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct RegisterContent<'info> {
    #[account(init_if_needed, payer = user, space = 9000, seeds = [content_hash_seed(content_hash.as_bytes())], bump)]
    pub content_registry: Account<'info, ContentRegistry>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct ReportInfringement<'info> {
    #[account(mut)]
    pub content_registry: Account<'info, ContentRegistry>,
    #[account(init, payer = reporter, space = 9000)]
    pub infringement_report: Account<'info, InfringementReport>,
    #[account(mut)]
    pub reporter: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct ContentRegistry {
    pub owner: Pubkey,
    pub content_hash: String,
    pub ipfs_url: String,
    pub timestamp: i64,
}

#[account]
pub struct InfringementReport {
    pub original_hash: String,
    pub infringing_url: String,
    pub reporter: Pubkey,
    pub timestamp: i64,
}

/// Seeds helper for deterministic content registry accounts
pub fn content_hash_seed(content_hash: &[u8]) -> &[u8] {
    content_hash
}

#[error_code]
pub enum ErrorCode {
    #[msg("This content hash is already registered.")]
    ContentAlreadyRegistered,
}
